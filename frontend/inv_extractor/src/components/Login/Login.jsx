import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import './Login.css'
const Login = () => {
    const [gstin , setGSTIN] = useState('')
    const [password , setPassword] = useState('')
    return (
        <>
            <div class="container">
                <h1>Login</h1>
                <form method="post" action="{% url 'login' %}">
                    <div class="form-group">
                        <label for="username">GSTIN / UIN</label>
                        <input type="text" value={gstin} onChange={(e)=>setGSTIN(e.target.value)} id="username" name="gstin" required />
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} id="password" name="password" required />
                    </div>
                    <button type="submit">Login</button>
                </form>
                <p>Don't have an account? <a href="{% url 'signup' %}">Sign up</a></p>
            </div>
        </>
    )
}

export default Login