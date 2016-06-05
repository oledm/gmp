import React from 'react';
import classNames from 'classnames'
import InputLabel from './label'
import Messages from './messages'

export default class InputText extends React.Component {
    render() {
        const { valid, error, touched, value, onBlur, onChange, ...rest } = this.props
        var classes = classNames(this.props.className, {
            'has-error': touched && !valid
        });

        return (
            <div className={classes}>
                <InputLabel htmlFor="order_number">{this.props.label}</InputLabel>
                <input
                    type="text"
                    id="order_number"
                    className="form-control"
                    required={!this.props.optional}
                    value={value}
                    onBlur={onBlur}
                    onChange={onChange}
                />
                <Messages
                    show={ touched && !valid }
                >
                    {error}
                </Messages>
            </div>
        )
    }
}
