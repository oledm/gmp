import React from 'react';
import classNames from 'classnames'
import Label from './Label'
import Messages from './Messages'

const InputWrapper = ({
    valid, error, touched, value, onBlur, onChange,
    className, id, label, children
}) => {
    const classes = classNames(className, {
        'has-error': touched && !valid
    });

    return (
        <div className={classes}>
            <Label htmlFor={id}>{label}</Label>
                {children}
            <Messages
                show={ touched && !valid }
            >
                {error}
            </Messages>
        </div>
    )
}
export default InputWrapper
