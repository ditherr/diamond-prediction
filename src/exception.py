import sys

# Custom Exception Function for the Project
def error_message_details(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info() # get the details of the error
    file_name = exc_tb.tb_frame.f_code.co_filename # get the file name
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


# Custom Exception Class for the Project
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail)

    def __str__(self):
        return self.error_message