import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'
import rootReducer from '../reducers/index'
import { redirect } from '../middlewares/redirect'

const configureStore = preloadedState =>
    createStore(
        rootReducer,
        preloadedState,
        compose(
            applyMiddleware(thunkMiddleware),
            applyMiddleware(redirect),
            window.devToolsExtension ? window.devToolsExtension() : f => f
        )
    )

export default configureStore
