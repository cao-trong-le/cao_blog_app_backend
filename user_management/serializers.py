from rest_framework import serializers
from .models import NewUser



class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    class Meta:
        model = NewUser
        fields = ('id', 'code', 'email', 'username', 'last_name', 'first_name', 'avatar')
        # extra_kwargs = {'password': {'write_only': True}}


class NewUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    # email = serializers.EmailField(required=False, write_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = NewUser
        fields = ('username', 'password', 'last_name', 'first_name')
        # extra_kwargs = {
        #     'email': {
        #         'write_only': True,
        #         'validators': []
        #     }
        # }
        
    def validate(self, data):
        check_list = ["username", "email"]
        error = {
            "type": None,
            "message": None
        }
        for check in check_list:
            if check == "username":
                user = self.Meta.model.objects.filter(username=data["username"])
                if user.exists():
                    error["type"] = "username"
                    error['message'] = "This username is already exist"
                    # if pass an object => ValidationError will create a field for each key
                    raise serializers.ValidationError(error)
            
            if check == "email":
                user = self.Meta.model.objects.filter(email=self.initial_data["email"])
                if user.exists():
                    error["type"] = "email"
                    error["message"] = "This email is already exist"
                    raise serializers.ValidationError(error)
                
        return data

    def create(self, request):
        # refine initial data
        password = self.validated_data.pop('password', None)
        
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**self.validated_data)
        instance.email = self.initial_data.get("email", None)
        instance.is_active = True
        
        # hash password
        if password is not None:
            instance.set_password(password)
        
        # get a list of files from FILES
        avatar = request.FILES.getlist("avatar")
    
        if len(avatar) > 0:
            instance.avatar = avatar[0]
        
        instance.save()
        
        return instance
    
    def update(self):
        pass