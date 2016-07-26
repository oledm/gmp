import React from 'react';
import InputWrapper from './InputWrapper'
import InputPure from './InputPure'
import v4 from 'node-uuid'

export default (props) => {
    const id = v4()
    const input = <InputPure id={id} {...props} />

    return (
        <InputWrapper {...props} id={id}>
            {props.icon ? 
                <div className="input-group">
                    <span className="input-group-addon">
                        <i className={"glyphicon glyphicon-" + props.icon}></i>
                    </span>
                    {input}
                </div>
                : 
                input
            }
	</InputWrapper>
    )
}
