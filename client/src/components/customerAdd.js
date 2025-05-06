import React from 'react';
import axios from 'axios';
import { 
    TextField, 
    Button, 
    Box, 
    Typography, 
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from '@mui/material';
import { withStyles } from '@mui/styles';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

const styles = {
    hidden: {
        display: 'none'
    }
};

class CustomerAdd extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            file: null,
            userName: '',
            birthday: '',
            gender: '',
            job: '',
            fileName: '',
            error: null,
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
            file: null,
            userName: '',
            birthday: '',
            gender: '',
            job: '',
            fileName: '',
            open: false
         });
    }
    
    

    handleFormSubmit = (e) => {
        e.preventDefault();
        
        // 유효성 검사
        if (!this.state.userName || !this.state.birthday || !this.state.gender || !this.state.job) {
            this.setState({ error: '모든 필드를 입력해주세요.' });
            return;
        }

        const formData = new FormData();
        formData.append('image', this.state.file);
        formData.append('name', this.state.userName);
        formData.append('birthday', this.state.birthday);
        formData.append('gender', this.state.gender);
        formData.append('job', this.state.job);

        axios.post('/api/customers', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log('성공:', response);
            this.setState({
                file: null,
                userName: '',
                birthday: '',
                gender: '',
                job: '',
                fileName: '',
                error: null,
                open: false
            });
            this.props.stateRefresh();
        })
        .catch(error => {
            console.error('에러:', error);
            this.setState({ error: '고객 추가 중 오류가 발생했습니다.' });
        });
    }

    handleFileChange = (e) => {
        this.setState({
            file: e.target.files[0],
            fileName: e.target.value
        });
    }

    handleValueChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
    }

    render() {
        const { classes } = this.props;
        return (
            <div>
                <Button variant="contained" color="primary" onClick={this.handleClickOpen}>고객 추가</Button>
                <Dialog open={this.state.open} onClose={this.handleClose}>
                    <DialogTitle>고객 추가</DialogTitle>
                    <DialogContent>
                        <input className={classes.hidden} accept="image/*" id="raised-button-file" type="file" file={this.state.file} value={this.state.fileName} onChange={this.handleFileChange} />
                        <label htmlFor="raised-button-file">
                            <Button variant="contained" color="primary" component="span">
                                {this.state.fileName === "" ? "프로필 이미지 선택" : this.state.fileName}
                            </Button>
                        </label>
                        <TextField label="이름" type="text" name="userName" value={this.state.userName} onChange={this.handleValueChange} />
                        <TextField label="생년월일" type="text" name="birthday" value={this.state.birthday} onChange={this.handleValueChange} />
                        <TextField label="성별" type="text" name="gender" value={this.state.gender} onChange={this.handleValueChange} />
                        <TextField label="직업" type="text" name="job" value={this.state.job} onChange={this.handleValueChange} />
                    </DialogContent>
                    <DialogActions>
                        <Button variant="contained" color="primary" onClick={this.handleFormSubmit}>추가</Button>
                        <Button variant="outlined" color="secondary" onClick={this.handleClose}>닫기</Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }

}

export default withStyles(styles)(CustomerAdd);
