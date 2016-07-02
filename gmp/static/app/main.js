import 'babel-polyfill'
import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux'
import { browserHistory, Router, Route, IndexRoute } from 'react-router'
import configureStore from './store/configureStore'
import App from './components/App'
import AuthForm from './components/forms/AuthForm'
import LoginForm from './components/forms/LoginForm'
import RegisterForm from './components/forms/RegisterForm'
import Dashboard from './components/Dashboard'
import requireAuthentication from './containers/AuthenticatedComponent'

const store = configureStore()

render(
    <Provider store={store}>
        <Router history={browserHistory}>
	    <Route path='/' component={App}>
                <IndexRoute component={requireAuthentication(Dashboard)} />
                <Route path='/login' component={AuthForm(LoginForm)} />
                <Route path='/register' component={AuthForm(RegisterForm)} />
	    </Route>
        </Router>
    </Provider>,
    document.getElementById('content')
)
