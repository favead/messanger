from flaskr.models import auth


def test_verivy_form():
  assert auth.verify_form({'username':'',}) == 'username is required'
  assert auth.verify_form({'username':'da'}) == 'username is required'
  assert auth.verify_form({'username':'danil5678444'}) == None

if __name__ == '__main__':
  test_verivy_form()