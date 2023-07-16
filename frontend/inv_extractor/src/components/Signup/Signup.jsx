import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import './Signup.css'
const Signup = () => {
    const [gstin , setGSTIN] = useState('')
    const [password , setPassword] = useState('')

    return (
        <div class="container">
            <h1>Sign up</h1>
            <form method="post" action="{% url 'signup' %}">
                <div class="form-group">
                    <label for="gstin">GSTIN:</label>
                    <input type="text" id="gstin" name="gstin" required />
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <button type="submit">Sign up</button>
            </form>
            <p>Already have an account? <a href="#">Signup</a></p>
        </div>
    )
}

export default Signup