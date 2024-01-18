import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tifffile
import os
class OptimizeRotateAngle():
    def __init__(self,
                tiff_path = None,
                rotate_angle_min = -1,
                rotate_angle_max = 1,
                rotate_angle_step = 0.01,
                frame_min = 0,
                frame_max = None):
        self.tiff_filename =  os.path.splitext(os.path.basename(tiff_path))[0]
        self.images_multiarr = tifffile.imread(tiff_path)
        self.rotate_angle_arr = np.arange(rotate_angle_min,rotate_angle_max,rotate_angle_step)
        
        self.optimize_angle = None
        if frame_max == None:
            frame_max = np.min( len(self.images_multiarr),frame_max)
        self.calc_sum_images_arr(frame_min,frame_max)
    
    def show_optimazed_image(self):
        optimized_image_arr = OptimizeRotateAngle.rotate_image(self.sum_images_arr,self.optimize_angle)
        sns.heatmap(optimized_image_arr,cmap='Greys_r')
    def to_tiff(self,angle=None,save_dir=None):
        if angle == None:
            angle = self.optimize_angle
        optimized_image_list = []
        for frame in range(len(self.images_multiarr)):
            optimized_image_list.append(OptimizeRotateAngle.rotate_image(self.images_multiarr[frame],angle))
        optimized_image_arr = np.array(optimized_image_list)
        if save_dir is None:
            tifffile.imwrite(f'rotated_({self.optimize_angle:.1e})_{self.tiff_filename}.tif',optimized_image_arr)
        else:
             tifffile.imwrite(f'{save_dir}/rotated_({angle:.1e})_{self.tiff_filename}.tif',optimized_image_arr)
    def calc_sum_images_arr(self,
                            frame_min,
                            frame_max):
        now_sum = np.zeros((512,512))
        for frame in range(frame_min,frame_max):
            now_sum = now_sum + self.images_multiarr[frame]
        self.sum_images_arr = now_sum
    def get_optimize_angle(self,
                           left_range_min = 100,
                           left_range_max = 200,
                           right_range_min = 350,
                           right_range_max = 450):
        
        left_peaks_symvalue_list = []
        right_peaks_symvalue_list = []
        for deg in self.rotate_angle_arr:
            rotated_image =  OptimizeRotateAngle.rotate_image(self.sum_images_arr, deg)
            insty_dist = np.sum(rotated_image,axis=1)
            left_peak_idx = OptimizeRotateAngle.find_peak_idx(insty_dist,left_range_min,left_range_max)
            right_peak_idx = OptimizeRotateAngle.find_peak_idx(insty_dist,right_range_min,right_range_max)
            left_peak_info = OptimizeRotateAngle.calculate_area_ratio_and_center(insty_dist, left_peak_idx,is_plot=False)
            right_peak_info = OptimizeRotateAngle.calculate_area_ratio_and_center(insty_dist, right_peak_idx,is_plot=False)
            left_peaks_symvalue_list.append(left_peak_info['Area Ratio'])
            right_peaks_symvalue_list.append(right_peak_info['Area Ratio'])
        
        fig = plt.figure(figsize=(10,10),dpi=150)
        ax_left= fig.add_subplot(221)
        ax_right = fig.add_subplot(222)
        ax_main = fig.add_subplot(212)
        
        left_barom_arr = np.abs(1 - np.array(left_peaks_symvalue_list))
        right_barom_arr = np.abs(1- np.array(right_peaks_symvalue_list))
        self.optimize_angle = self.rotate_angle_arr[np.argmin(left_barom_arr/np.max(left_barom_arr) + right_barom_arr/np.max(right_barom_arr))]

        ax_left.plot(self.rotate_angle_arr,left_barom_arr,label='left barometer')
        ax_right.plot(self.rotate_angle_arr,right_barom_arr,label='right barometer')
        ax_main.plot(self.rotate_angle_arr,left_barom_arr/np.max(left_barom_arr) + right_barom_arr/np.max(right_barom_arr),label='left + right barometer')
        ax_main.axvline(self.optimize_angle,linestyle='--',color='#FF0000')
        ax_left.legend()
        ax_right.legend()
        ax_main.legend()
        ax_main.set_xlabel('Rotate Angle(deg)')
        ax_main.set_ylabel('Barometer Value')
        
        
    @staticmethod
    def read_tiff_with_opencv(tiff_path):
    # TIFFファイルから複数の画像を読み込む
        retval, images_multiarr = cv2.imreadmulti(tiff_path, [], cv2.IMREAD_ANYDEPTH)

        # すべての画像が正常に読み込まれたことを確認
        if not retval:
            raise ValueError("画像の読み込みに失敗しました。")
        return images_multiarr
    
    def plot_single_frame(self,frame_num=0):
        sns.heatmap(self.images_multiarr[frame_num],cmap='Greys_r')
        plt.show()
    
    @staticmethod
    def rotate_image(image, angle):
        """
        画像を指定された角度だけ回転させる。

        :param image: 回転させる画像（NumPy配列）
        :param angle: 回転角度（度単位）
        :return: 回転された画像
        """
        # 画像の中心を計算
        center = (image.shape[1] / 2, image.shape[0] / 2)

        # 回転行列を取得
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # 画像を回転
        rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

        return rotated_image
    
    @staticmethod
    def find_peak_idx(data,range_min,range_max):
        peak_data = data[range_min : range_max]
        peak_idx = np.argmax(peak_data) + range_min
        return peak_idx
    
    @staticmethod
    def find_fwhm(data, peak_index):
        """
        Find the indices of the Full Width at Half Maximum (FWHM) for a peak.
        """
        peak_height = data[peak_index]
        third_max = peak_height / 3

        # Find the left side of FWHM
        left_index = peak_index
        while left_index > 0 and data[left_index] > third_max:
            left_index -= 1

        # Find the right side of FWHM
        right_index = peak_index
        while right_index < len(data) and data[right_index] > third_max:
            right_index += 1

        return left_index, right_index
    
    @staticmethod
    def calculate_area_ratio(data, left_index, right_index, peak_index):
        """
        Calculate the area ratio of a peak within the FWHM.
        """
        left_area = np.sum(data[left_index:peak_index])
        right_area = np.sum(data[peak_index:right_index])
        area_ratio = left_area / right_area if right_area != 0 else np.nan  # Avoid division by zero

        return area_ratio, left_area, right_area
    
    @staticmethod
    def calculate_area_ratio_and_center(data, peak_idx,is_plot=True):
        """
        Calculate the area ratio for a peak at a specified index and visualize the process.
        """
        left_idx, right_idx = OptimizeRotateAngle.find_fwhm(data, peak_idx)
        area_ratio, left_area, right_area = OptimizeRotateAngle.calculate_area_ratio(data, left_idx, right_idx, peak_idx)

        # Visualize the left and right area
        if is_plot:
            plt.figure(figsize=(6, 6))
            plt.plot(data, label='Data')
            plt.fill_between(range(left_idx, peak_idx+1), data[left_idx:peak_idx+1], label='Left Area', alpha=0.5)
            plt.fill_between(range(peak_idx, right_idx+1), data[peak_idx:right_idx+1], label='Right Area', alpha=0.5)
            plt.axvline(x=peak_idx, color='r', linestyle='--', label='Peak')
            plt.title('Peak with FWHM Areas')
            plt.xlabel('Index')
            plt.ylabel('Value')
            plt.xlim(left_idx-30,right_idx+30)
            plt.legend()
            plt.show()

        return {'Area Ratio': area_ratio, 'Center Index': peak_idx}
    