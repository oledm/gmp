import React from 'react'
import LoginRegisterForm from './LoginRegisterForm'

const AuthForm = Component => {
        
    const WrapedComponent = () => (
        <LoginRegisterForm>
            <Component />
        </LoginRegisterForm>
    )

    return WrapedComponent
}

export default AuthForm
