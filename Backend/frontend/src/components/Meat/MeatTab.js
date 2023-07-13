import {useState, useEffect} from "react";
import styles from "./MeatTab.module.css";
import TabBtns from "./TabBtns";
import Table from 'react-bootstrap/Table';


//tab 버튼 별 데이터 설정
function MeatTab({fresh, heated , lab_data, tongue, apiData}){
    const [currentTab , setCurrentTab] = useState("");
    const [data, setData] = useState({});
    // 클릭한 tab을 가져오고 tab한 버튼에 따른 데이터를 가져옴 
    const currentTabHandler = (tab)=>{
        fetchDataToTab(tab);
        setCurrentTab(tab);
    }

    // tab버튼에 따라서 보여줄 data를 다르게 set함
    const fetchDataToTab =(currentTab)=> {//async(pageNum) =>{\
        switch(currentTab){
            case "firstBtn":
                setData((heated));
                break;
            case "secondBtn":
                setData((fresh));
                break;
            case "thirdBtn":
                setData((tongue));
                break;
            case "fouthBtn":
                setData((lab_data));
                break;
            case "fifthBtn":
                setData((apiData));
                break;
            default:
                setData((null));
                break;
        }
    }

    return (
      <div>
        <TabBtns
          currentTab={currentTab}
          currentTabHandler={currentTabHandler}
        />
        <Table striped bordered hover>
          {data ? (
            <tbody>
              {Object.entries(data).map(([key, value]) => {
                return (
                  <tr>
                    <td style={{ width: "30%" }}>{key}</td>
                    <td>{value}</td>
                  </tr>
                );
              })}
            </tbody>
          ) : (
            "{}"
          )}
        </Table>
      </div>
    );
}

export default MeatTab;