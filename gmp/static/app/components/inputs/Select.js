import React from 'react';
import InputWrapper from './InputWrapper'
import v4 from 'node-uuid'

export default (props) => {
    const id = v4()
    const select = (
        <select
            id={id}
            className="form-control"
            value={props.value || ''}
            onBlur={props.onBlur}
            onChange={props.onChange}
        >
            {props.children}
        </select>
    )

    return (
        <InputWrapper {...props} id={id}>
            {props.icon ? 
                <div className="input-group">
                    <span className="input-group-addon">
                        <i className={"glyphicon glyphicon-" + props.icon}></i>
                    </span>
                    {select}
                </div>
                : 
                select
            }
        </InputWrapper>
    )
}
