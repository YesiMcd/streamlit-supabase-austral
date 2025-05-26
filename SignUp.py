import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import re

# Configuración
st.set_page_config(page_title="SuperListo - Sign Up", layout="wide")

# CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 2.5rem !important;
    }
    .main {
        background-color: rgb(193, 208, 209);
    }
    
    /* Estilos para el formulario */
    .signup-form-container {
        background: linear-gradient(135deg, #00ecc2 0%, #0078ff 50%, #ff8a25 75%, #ff4356 100%);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin: 20px auto;
        max-width: 800px;
    }

    .signup-title {
        color: white;
        font-size: 42px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    .form-row {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }

    .form-group {
        flex: 1;
    }

    .form-label {
        color: white;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 8px;
        display: block;
    }

    .form-input {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.9);
        font-size: 16px;
        transition: all 0.3s ease;
    }

    .form-input:focus {
        border-color: #0078ff;
        box-shadow: 0 0 0 3px rgba(0, 120, 255, 0.2);
        outline: none;
    }

    .form-input.error {
        border-color: #ff4356;
    }

    .error-message {
        color: #ff4356;
        font-size: 14px;
        margin-top: 5px;
        display: none;
    }

    .payment-methods {
        display: flex;
        gap: 15px;
        margin-top: 10px;
    }

    .payment-method {
        flex: 1;
        padding: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.9);
        cursor: pointer;
        text-align: center;
        transition: all 0.3s ease;
    }

    .payment-method:hover {
        background-color: rgba(255, 255, 255, 1);
        transform: translateY(-2px);
    }

    .payment-method.selected {
        border-color: #0078ff;
        background-color: #0078ff;
        color: white;
    }

    .submit-button {
        background-color: #0078ff;
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin-top: 30px;
        transition: all 0.3s ease;
    }

    .submit-button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }

    .login-link {
        text-align: center;
        margin-top: 20px;
        color: white;
    }

    .login-link a {
        color: #00ecc2;
        text-decoration: none;
        font-weight: 600;
    }

    .login-link a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript para validación
st.markdown("""
    <script>
    function validateForm(event) {
        event.preventDefault();
        let isValid = true;
        
        // Validar nombre y apellido (solo letras)
        const nameRegex = /^[A-Za-z\s]+$/;
        const firstName = document.getElementById('firstName');
        const lastName = document.getElementById('lastName');
        
        if (!nameRegex.test(firstName.value)) {
            document.getElementById('firstNameError').style.display = 'block';
            firstName.classList.add('error');
            isValid = false;
        } else {
            document.getElementById('firstNameError').style.display = 'none';
            firstName.classList.remove('error');
        }
        
        if (!nameRegex.test(lastName.value)) {
            document.getElementById('lastNameError').style.display = 'block';
            lastName.classList.add('error');
            isValid = false;
        } else {
            document.getElementById('lastNameError').style.display = 'none';
            lastName.classList.remove('error');
        }
        
        // Validar email
        const email = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            document.getElementById('emailError').style.display = 'block';
            email.classList.add('error');
            isValid = false;
        } else {
            document.getElementById('emailError').style.display = 'none';
            email.classList.remove('error');
        }
        
        // Validar código postal (solo números)
        const postalCode = document.getElementById('postalCode');
        const postalRegex = /^\d+$/;
        if (!postalRegex.test(postalCode.value)) {
            document.getElementById('postalCodeError').style.display = 'block';
            postalCode.classList.add('error');
            isValid = false;
        } else {
            document.getElementById('postalCodeError').style.display = 'none';
            postalCode.classList.remove('error');
        }
        
        // Validar dirección
        const address = document.getElementById('address');
        if (!address.value.trim()) {
            document.getElementById('addressError').style.display = 'block';
            address.classList.add('error');
            isValid = false;
        } else {
            document.getElementById('addressError').style.display = 'none';
            address.classList.remove('error');
        }
        
        // Validar método de pago
        const paymentMethod = document.querySelector('input[name="payment"]:checked');
        if (!paymentMethod) {
            document.getElementById('paymentError').style.display = 'block';
            isValid = false;
        } else {
            document.getElementById('paymentError').style.display = 'none';
        }
        
        return isValid;
    }

    function selectPaymentMethod(method) {
        document.querySelectorAll('.payment-method').forEach(el => {
            el.classList.remove('selected');
        });
        document.getElementById(method).classList.add('selected');
        document.getElementById(method + 'Radio').checked = true;
    }
    </script>
""", unsafe_allow_html=True)

# Formulario de registro
st.markdown("""
    <div class="signup-form-container">
        <h1 class="signup-title">Create Your Account</h1>
        <form id="signupForm" onsubmit="return validateForm(event)">
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label" for="firstName">First Name</label>
                    <input type="text" id="firstName" class="form-input" placeholder="Enter your first name">
                    <div id="firstNameError" class="error-message">Please enter a valid first name (letters only)</div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="lastName">Last Name</label>
                    <input type="text" id="lastName" class="form-input" placeholder="Enter your last name">
                    <div id="lastNameError" class="error-message">Please enter a valid last name (letters only)</div>
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="email">Email</label>
                <input type="email" id="email" class="form-input" placeholder="Enter your email">
                <div id="emailError" class="error-message">Please enter a valid email address</div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label" for="postalCode">Postal Code</label>
                    <input type="text" id="postalCode" class="form-input" placeholder="Enter your postal code">
                    <div id="postalCodeError" class="error-message">Please enter a valid postal code (numbers only)</div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="address">Address</label>
                    <input type="text" id="address" class="form-input" placeholder="Enter your address">
                    <div id="addressError" class="error-message">Please enter your address</div>
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Payment Method</label>
                <div class="payment-methods">
                    <div class="payment-method" id="debit" onclick="selectPaymentMethod('debit')">
                        <input type="radio" name="payment" id="debitRadio" value="debit" style="display: none;">
                        <span>Debit Card</span>
                    </div>
                    <div class="payment-method" id="credit" onclick="selectPaymentMethod('credit')">
                        <input type="radio" name="payment" id="creditRadio" value="credit" style="display: none;">
                        <span>Credit Card</span>
                    </div>
                    <div class="payment-method" id="cash" onclick="selectPaymentMethod('cash')">
                        <input type="radio" name="payment" id="cashRadio" value="cash" style="display: none;">
                        <span>Cash</span>
                    </div>
                </div>
                <div id="paymentError" class="error-message">Please select a payment method</div>
            </div>
            
            <button type="submit" class="submit-button">Create Account</button>
            
            <div class="login-link">
                Already have an account? <a href="Inicio.py">Sign In</a>
            </div>
        </form>
    </div>
""", unsafe_allow_html=True) 