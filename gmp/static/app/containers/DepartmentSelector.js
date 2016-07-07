import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { fetchDepartments } from '../actions/index'
import Select from '../components/inputs/Select'

class DepartmentSelector extends Component {
    componentWillMount() {
        this.props.dispatch(fetchDepartments())
    }

    render() {
        const { departments, ...rest } = this.props
        return (
            <Select {...rest}>
                <option value=''></option>
                {departments.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
            </Select>
        )
    }
}

DepartmentSelector.propTypes = {
    departments: React.PropTypes.array.isRequired,
    label: React.PropTypes.string,
    className: React.PropTypes.string
}

const mapStateToProps = (state) => ({
    departments: state.departments.departments
})

export default connect(mapStateToProps)(DepartmentSelector)
