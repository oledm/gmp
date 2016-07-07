import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'
import rootReducer from '../reducers/index'
import { redirect } from '../middlewares/redirect'

const globalStore = {};
function getHotReloadStore(key) {
  if (globalStore[key] === undefined) {
    globalStore[key] = {};
  }
  return globalStore[key];
}

const hotStore = getHotReloadStore('gmp:store');

let prevState;
if (hotStore.prevStore) {
  prevState = hotStore.prevStore.getState(); 
}

//export default function configureStore(reducers, initialState = prevState) {
//  const store = createStore(reducers, initialState); 
//  hotStore.prevStore = store;
//  return store;
//}

const configureStore = (preloadedState = prevState) => {
    const store = createStore(
        rootReducer,
        preloadedState,
        compose(
            applyMiddleware(thunkMiddleware),
            applyMiddleware(redirect),
            window.devToolsExtension ? window.devToolsExtension() : f => f
        )
    )
    hotStore.prevStore = store;
    return store;
}

export default configureStore
