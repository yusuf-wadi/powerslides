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

deta = Deta(str(cfg('DETA_KEY')))

db = deta.Base('users')

def update_credentials():
    return

# credit system
default_creds = 5

def register_user():
    with st.sidebar:
        with st.form('Register user'):
            st.markdown("<h3>🔐 Register</h3>", unsafe_allow_html=True)
            email = st.text_input('Email')
            username = st.text_input('Username').strip()
            name = st.text_input('Name')
            password = st.text_input('Password', type='password')
            confirm_password = st.text_input('Confirm password', type='password')
            if password != confirm_password:
                st.error('Passwords do not match')
            submitted = st.form_submit_button('Complete registration', on_click=register_user)
            if submitted and email and username and name and password and confirm_password and verify_email(email)[1]:
                if db.insert({'password': hasher._hash(hasher,password), 'name': name, 'email': email, "credits": default_creds},key=username):
                    st.success('User registered successfully')
                else:
                    st.error('User registration failed, username may already exist')
            elif submitted and not verify_email(email)[1]:
                st.error('Email is invalid')
            elif submitted:
                st.error('Please fill in all fields')
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
        emailinfo = validate_email(email, check_deliverability=False)

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
        
def verify_login(password):
    return
    
def login():

    st.markdown("<h3>🔐 Login</h3>", unsafe_allow_html=True)
    
    with st.form('Login'):
        st.session_state["username"] = st.text_input('Username').strip()
        password = st.text_input('Password', type='password')
        login_button = st.form_submit_button('Login')
    
    if login_button:   
        if db.get(st.session_state["username"]) is None:
            st.session_state["authentication_status"] = False
        elif bcrypt.checkpw(password.encode(),db.get(st.session_state["username"])['password'].encode()):
            st.session_state["authentication_status"] = True
            st.session_state["name"] = db.get(st.session_state["username"])['name']
            st.session_state["credits"] = db.get(st.session_state["username"])['credits']
        else:
            st.session_state["authentication_status"] = False
                
    if st.session_state["authentication_status"]:
        st.success('Login successful') 
    elif st.session_state["authentication_status"] is False:
         st.error('Username/password is incorrect')
    #     st.button('Reset Password', on_click=reset_password)
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    st.markdown("---")
    st.markdown("No account? Register below 👇")
    st.button('Register', on_click=register_user)
    
    
