from plot_dist_color_map_control import plotDistColorMap
class PlotTempResult():
    def __init__(self,dist_filepath=None):
        self.fig = None
        self.filepath = None
        self.temp_df = plotDistColorMap.format_dist_df(dist_filepath)
    """
    1. distファイルを取りに行く(これはtkinter側の都合なので、ここでは取りに行かない)
    2. plot_dist_のクラスメソッドを再利用してdfを整備
    3. up_temp_df,down_temp_dfに分ける
    4. plotOptionから種々の値を取得しに行く
    """
    @staticmethod
    def get_down_df():
        pass
if __name__ =='__main__':
    print('!TEST!')
