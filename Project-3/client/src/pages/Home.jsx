import { Button, Container, Modal } from '@mui/material';
import React, { useState } from 'react';
import LoginModal from '../components/home/LoginModal';
import SignupModal from '../components/home/SignupModal';

const Home = () => {
  const [logOpen, setLog] = useState(false)
  const [regOpen, setReg] = useState(false)

  const handleLogOpen = () =>{
    setLog(true)
  }

  const handleLogClose = () =>{
    setLog(false)
  }

  const handleRegOpen = () =>{
    setReg(true)
  }

  const handleRegClose = () =>{
    setReg(false)
  }

  return (
       <Container maxWidth='auto'
             style={{
                 backgroundColor: 'lightgrey',
                 minHeight: '100vh',
                 display: 'flex',
                 flexDirection: 'column',
                 alignItems: 'center',
                 justifyContent: 'center',
                 borderRadius: '10px',
             }}>
         <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <Button
              onClick={handleLogOpen}
              variant="contained"
              color="primary"
              sx={{ width: '150px', height: '50px' }}
            >
              Login
            </Button>
            <Button
              onClick={handleRegOpen}
              variant="contained"
              color="primary"
              sx={{ width: '150px', height: '50px' }}
            >
              Register
            </Button>
             <Modal
                open={logOpen}
                aria-labelledby='modal-modal-title'
                aria-describedby='modal-modal-description'>
                    <div>
                        <LoginModal open={logOpen} handleClose={handleLogClose} />
                    </div>
             </Modal>
             <Modal
                open={regOpen}
                aria-labelledby='modal-title'
                aria-describedby='modal-description'>
                    <div>
                        <SignupModal open={regOpen} handleClose={handleRegClose} />
                    </div>
             </Modal>
         </div>
       </Container>
  )
}

export default Home