import React from 'react'
import TabLink from '../TabLink'

const LoginRegisterForm = ({ children }) => (
    <div>
        <ul className="nav nav-tabs">
            <TabLink to="/login">Вход</TabLink>
            <TabLink to="/register">Регистрация</TabLink>
        </ul>

        {children}
    </div>
)

LoginRegisterForm.propTypes = {
    children: React.PropTypes.element.isRequired
}

export default LoginRegisterForm
