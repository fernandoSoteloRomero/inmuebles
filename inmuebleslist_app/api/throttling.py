from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ComentarioCreateThrottle(UserRateThrottle):
  scope = 'comentario_create'
  
  
  
  
class ComentarioListThrottle(UserRateThrottle):
  scope = 'comentario_list'