
class Output():
    def __init__(self, number_of_single, number_of_double, average_area_single, average_area_double):
        self.number_of_single = number_of_single
        self.number_of_double = number_of_double
        self.average_area_single = average_area_single
        self.average_area_double = average_area_double
    def toJson(self, result_image_link):
        dict = {}
        dict['numberOfSingle'] = self.number_of_single
        dict['numberOfDouble'] = self.number_of_double
        dict['averageAreaSingle'] = self.average_area_single
        dict['averageAreaDouble'] = self.average_area_double
        dict['resultImage'] = result_image_link
        return dict
