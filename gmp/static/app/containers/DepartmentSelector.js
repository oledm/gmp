import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { fetchDepartments } from '../actions/index'
import Select from '../components/inputs/Select'

class DepartmentSelector extends Component {
    constructor(props) {
        super(props)
        props.dispatch(fetchDepartments())
    }

    render() {
        const { options, ...rest } = this.props
        return (
            <Select {...rest}>
                <option value=""></option>
                {options.map(o => <option key={o.id} value={o.name}>{o.name}</option>)}
            </Select>
        )
    }
}

DepartmentSelector.propTypes = {
    options: React.PropTypes.array.isRequired
}

const mapStateToProps = (state) => ({
    options: state.departments.departments
})

export default connect(mapStateToProps)(DepartmentSelector)