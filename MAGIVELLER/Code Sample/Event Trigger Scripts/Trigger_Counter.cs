using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Trigger_Counter : MonoBehaviour
{

    public int Trigger_Count = 0;
    public int Target_Trigger_Count = 3;
    


    // Update is called once per frame
    void Update()
    {
        if (Trigger_Count == Target_Trigger_Count)
        {
            GameObject ChildObject;
            ChildObject = this.transform.GetChild(0).gameObject;
            ChildObject.SetActive(true);

        }
    }
}
