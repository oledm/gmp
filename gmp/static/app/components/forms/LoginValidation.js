import memoize from 'lru-memoize';
import {createValidator, required, integer, maxLength, email} from '../../utils/validator';

const rules = createValidator({
    email: [required, email],
//    email: [required, email],
//    age: [required, integer],
    password: [required],
});

export default memoize(10)(rules)
