import 'babel-polyfill'
import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux'
import configureStore from './store/configureStore'
import App from './components/App'
import LoginForm from './components/forms/LoginForm'

const store = configureStore()

render(
    <Provider store={store}>
    <div>
        <App />
        <LoginForm />
    </div>
    </Provider>,
    document.getElementById('content')
)
