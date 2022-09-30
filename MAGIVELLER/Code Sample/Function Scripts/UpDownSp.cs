using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UpDownSp : MonoBehaviour
{
    public bool IsSelf;
    public GameObject ControlObj;

    public float Speed;

    public float TargetVal;
    // Start is called before the first frame update
    void Start()
    {
        if (IsSelf)
        {
            ControlObj = this.gameObject;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnCollisionStay(Collision collision)
   
    {
        if (collision.gameObject.tag == "Player")
        {
            if (Mathf.Abs(ControlObj.transform.position.y - TargetVal) > 1)
            {
                ControlObj.transform.position += new Vector3(0, Speed, 0);
            }
            else
            {
                ControlObj.transform.position = new Vector3(ControlObj.transform.position.x, TargetVal, ControlObj.transform.position.z);
            }
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.gameObject.tag == "Player")
        {
            if (Mathf.Abs(ControlObj.transform.position.y - TargetVal) > 1)
            {
                ControlObj.transform.position += new Vector3(0, Speed, 0);
            }
            else
            {
                ControlObj.transform.position = new Vector3(ControlObj.transform.position.x, TargetVal, ControlObj.transform.position.z);
            }
        }
    }
}
