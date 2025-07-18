from locust import HttpUser,task,between

class QuikStartUser(HttpUser):

    def on_start(self):
        response=self.client.post('/accounts/api/v1/jwt/create/',data={
            'email':'test@test.com',
            'password':'mxgyuirt22ali'
        }).json()
        self.client.headers = {'Authorization' : f'Bearer {response.get('access',None)}'}

    @task
    def post_list(self):
        self.client.get('/blog/api/v1/posts/')
    
    @task
    def category_list(self):
        self.client.get('/blog/api/v1/category/')