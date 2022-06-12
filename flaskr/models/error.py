class FlaskrError(Exception):
  def __init__(self, error_message: str):
    self.error_message = error_message
    super().__init__(self.error_message)

  def __str__(self):
    return f"{self.error_message}"