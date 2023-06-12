import streamlit as st
from components.landing import landing
from streamlit_authenticator import Hasher as hasher
import email as em
import string
import random
from deta import Deta
from decouple import config as cfg
from email_validator import validate_email, EmailNotValidError
import bcrypt
#from src.verify_phone import _verify_phone
#import pyotp
import phonenumbers


# setup vars

#totp = pyotp.TOTP('base32secret3232')

deta = Deta(str(cfg('DETA_KEY')))

db = deta.Base('users')

def update_credentials():
    return

# credit system: currently slides created
default_creds = 0
###


def register_user():

    with st.form('Register user'):
        st.markdown("<h3>🔐 Register</h3>", unsafe_allow_html=True)
        email = st.text_input('Email')
        # only allow numbers
        #phone = st.text_input('Phone number')
        username = st.text_input('Username').strip()
        name = st.text_input('Name')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm password', type='password')
        submit = st.form_submit_button('Register')
        
        if submit:
            if password != confirm_password:
                st.error('Passwords do not match')
            if username != "":
                if db.get(username):
                    st.error('Username already exists')
                    username = ""
                    
            if verify_email(email)[1]:
                if len(db.fetch({'email': email}).items) > 0:
                    st.error('Email already exists')
                    email = ""
            else:
                st.error('Invalid email')
                email = ""
                
            # if phone != "":
            #     check_phone = phone
            #     try:
            #         if not phonenumbers.is_valid_number(phonenumbers.parse(check_phone, "US")):
            #             st.error('Invalid phone number')
            #             phone = ""
            #     except Exception as e:
            #         st.error('Invalid phone number')
            #         phone = ""
            #     if len(db.fetch({'phone': check_phone}).items) > 0:
            #         st.error('Phone number already exists')
            #         phone = ""
            
            push_user(email,username,name,password)#phone)
        
def push_user(email,username,name,password):#phone):
    if username != "" and email != "" and name != "" and password != "":
            hashed_password = hasher._hash(hasher, password)
            if db.insert({
                'email': email,
                #'phone': phone,
                'name': name,
                'password': hashed_password,
                'credits': default_creds
            },
                    key=username):
                
                st.success('User registered successfully')
            else:
                st.error('Error registering user')
    else:
        st.warning('Please fill in all fields')
            
    # try:
    #     if authenticator.register_user('Register user', location='main', preauthorization=False):
            
    #         if verified():
    #             update_credentials()
    #             st.success('User registered successfully')
    # except Exception as e:
    #     st.error(e)
    

def verify_email(email):
    try:

        # Check that the email address is valid. Turn on check_deliverability
        # for first-time validations like on account creation pages (but not
        # login pages).
        emailinfo = validate_email(email, check_deliverability=True)

        # After this point, use only the normalized form of the email address,
        # especially before going to a database query.
        email = emailinfo.normalized
        return email,True
    
    except EmailNotValidError as e:

        # The exception message is human-readable explanation of why it's
        # not a valid (or deliverable) email address.
        print(str(e))
        return email,False
        

def verified(email) -> bool:
    # send email verification
    # generate random timed alphanumeric code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # send email
    
    em.message_from_string(f'Your verification code is {code}')
    
    return True
    
    
# def reset_password():
#     username = st.text_input('Username')
    
#     #check if username exists
#     if username not in authenticator.credentials.keys():
#         st.error('Username does not exist')
#         return

#     try:
#         if authenticator.reset_password(username, 'Reset password'):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)
 
def set_auth_status(status):
    st.session_state["authentication_status"] = status
    
def login_register():
    
    login_t, register_t = st.tabs(['Login', 'Register'])

    with login_t:
        st.markdown("<h3>🔐 Login</h3>", unsafe_allow_html=True) 
        with st.form('Login'):
            st.session_state["username"] = st.text_input('Username').strip()
            password = st.text_input('Password', type='password')
            login_button = st.form_submit_button('Login')
        
        if login_button:
            with st.spinner('Authenticating...'): 
                if db.get(st.session_state["username"]) is None:
                    st.session_state["authentication_status"] = False
                elif bcrypt.checkpw(password.encode(),db.get(st.session_state["username"])['password'].encode()):
                    st.session_state["name"] = db.get(st.session_state["username"])['name']
                    st.session_state["credits"] = db.get(st.session_state["username"])['credits']
                    set_auth_status(True)
                else:
                    set_auth_status(False)
                    
        if st.session_state["authentication_status"]:
            st.success('Login successful, press login again') 
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        #     st.button('Reset Password', on_click=reset_password)
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
    with register_t:
        register_user()
    

