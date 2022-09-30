using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Statue_Spinning : MonoBehaviour
{
    public KeyCode ConfirmKey; //KeyCode Preset
    public GameObject ButtonPress; //preset a empty public object
    public GameObject TargetEffect;
    public int PhaseNumber = 1; 
    public bool isActive = false; 
    
    void OnTriggerStay(Collider other)
    {
        if(other.gameObject.tag == "Player")//find object "player"
        {
            ButtonPress.SetActive(true);//When player press the bottom, set "true"

            if (Input.GetKey(ConfirmKey) && this.transform.Find("Object").gameObject.GetComponent<Animator>().GetCurrentAnimatorStateInfo(0).normalizedTime >= 1)
            { //gameObject start call animator

                switch (PhaseNumber)
                {
                    case 1:
                        this.transform.Find("Object").gameObject.GetComponent<Animator>().Play("Statue_Spinning_Stage_01");
                        isActive = false;
                        PhaseNumber ++;
                        break;
                    //When switch to case1, play "Statue_Spinning_Stage_01"
                    case 2:
                        this.transform.Find("Object").gameObject.GetComponent<Animator>().Play("Statue_Spinning_Stage_02");
                        isActive = true;
                        TargetEffect.GetComponent<Trigger_Counter>().Trigger_Count++;
                        PhaseNumber ++;
                        break;
                        //When switch to case1, play "Statue_Spinning_Stage_02"
                    case 3:
                        this.transform.Find("Object").gameObject.GetComponent<Animator>().Play("Statue_Spinning_Stage_03");
                        isActive = false;
                        TargetEffect.GetComponent<Trigger_Counter>().Trigger_Count--;
                        PhaseNumber = 1;
                        break;
                        //When switch to case1, play "Statue_Spinning_Stage_03"
                    default:
                        break;
                }
            }
        }
    }

    void OnTriggerExit(Collider other)
    {
        if (other.gameObject.tag == "Player")
        {
            ButtonPress.SetActive(false);
        }
    }


}
