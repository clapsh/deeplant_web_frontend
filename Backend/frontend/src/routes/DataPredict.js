import { useState, useEffect } from "react";
import { useParams, useLocation ,Link } from "react-router-dom";
import { Box, Typography, Button, IconButton} from '@mui/material';
import "bootstrap/dist/css/bootstrap.css"; 
import { FaAngleDoubleLeft } from "react-icons/fa";
import { DataLoad } from "../components/SingleData/SingleDataLoad";
function DataPredict(){
    //현재 로그인한 유저 이메일
    const [currentUser, setCurrUser] = useState("admin@admin.com");

    //로그인한 관리자의 관리번호 받아오기
    //const {editId} = useParams();
    //관리번호
     const idParam  = useParams();

    return (
      <Box sx={{ display: "flex"}}>
        <Box sx={style.fixed}>
          <div style={{display:'flex', alignItems:'center', marginLeft:'10px'}}>
            <Link to={{pathname : '/PA'}} >
              <IconButton sx={{backgroundColor:'white'}} size="large">
              <FaAngleDoubleLeft/>
              </IconButton>
            </Link>
          </div>
        </Box>
        {DataLoad(idParam.id, "예측", currentUser)}
        
      </Box>
    );
}
export default DataPredict;

const style={
  fixed:{
    position: 'fixed', 
    top:'70px',
    right:'0',
    left:'65px',
    zIndex: 1,
    width:'fit-content',
    borderRadius:'0',
    display:'flex',
    justifyContent:'space-between',
    backgroundColor:'#F5F5F5',
    height: "70px",
  },

}
