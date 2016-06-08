import 'babel-polyfill'
import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux'
import configureStore from './store/configureStore'
import App from './components/App'
import LoginForm from './components/forms/LoginForm'
import { browserHistory, Router, Route, IndexRoute } from 'react-router'

const store = configureStore()

render(
    <Provider store={store}>
        <Router history={browserHistory}>
	    <Route path='/' component={App}>
	    </Route>
        </Router>
    </Provider>,
    document.getElementById('content')
)
