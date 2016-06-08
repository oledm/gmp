import { LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILED } from '../actions/index'

const auth = (state = {
    isAuthenticated: false,
    isPending: false,
    error: '',
    token: ''
}, action) => {
    console.log('auth reducer with action', action.type)
    switch(action.type) {
        case LOGIN_REQUEST:
            console.log('LOGIN_REQUEST')
            return {...state,
                isPending: true
            }
        case LOGIN_SUCCESS:
            return {...state,
                isPending: false,
                isAuthenticated: true
            }
        case LOGIN_FAILED:
            return {...state,
                error: action.error
            }
        default:
            return state
    }
}

export default auth
