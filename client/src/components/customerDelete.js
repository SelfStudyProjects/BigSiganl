import React from 'react';
import axios from 'axios';
import { 
    Button, 
    Box, 
    Typography, 
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from '@mui/material';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

class CustomerDelete extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false
        }
    }

    handleClickOpen = () => {
        this.setState({ 
            open: true 
        });
    }

    handleClose = () => {
        this.setState({ 
            open: false
         });
    }

    deleteCustomer(id) {
        const url = '/api/customers/' + id;
        axios.delete(url)
            .then((response) => {
                this.props.stateRefresh();
            });
    }

    render() {
        return (
            <div>
                <Button variant="contained" color="secondary" onClick={this.handleClickOpen}>삭제</Button>
                <Dialog open={this.state.open} onClose={this.handleClose}>
                    <DialogTitle>삭제 경고</DialogTitle>
                    <DialogContent>
                        <Typography gutterBottom>
                            선택한 고객 정보가 삭제됩니다.
                        </Typography>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => this.deleteCustomer(this.props.id)} color="primary">삭제</Button>
                        <Button variant="outlined" onClick={this.handleClose} color="primary">닫기</Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default CustomerDelete;