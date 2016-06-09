import {
    LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILED,
    LOGOUT_REQUEST, LOGOUT_SUCCESS, LOGOUT_FAILED,

} from '../constants/index'

const auth = (state = {
    isAuthenticated: false,
    isPending: false,
    error: '',
    token: ''
}, action) => {
    switch(action.type) {
        case LOGIN_REQUEST:
        case LOGOUT_REQUEST:
            return {...state,
                isPending: true
            }
        case LOGIN_SUCCESS:
            return {...state,
                isPending: false,
                isAuthenticated: true
            }
        case LOGIN_FAILED:
        case LOGOUT_FAILED:
            return {...state,
                isPending: false,
                error: action.error
            }
        case LOGOUT_SUCCESS:
            return {...state,
                isPending: false,
                isAuthenticated: false
            }
        default:
            return state
    }
}

export default auth
