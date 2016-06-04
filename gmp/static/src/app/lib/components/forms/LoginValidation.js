import memoize from 'lru-memoize';
import {createValidator, required, integer, maxLength, email} from '../../utils/validator';

const rules = createValidator({
    username: [required, maxLength(10)],
    email: [required, email],
    age: [required, integer]
});

export default memoize(10)(rules)
