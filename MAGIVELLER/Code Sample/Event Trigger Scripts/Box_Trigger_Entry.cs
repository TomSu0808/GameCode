using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Box_Trigger_Entry : MonoBehaviour
{


    
    // Start is called before the first frame update
    void Start()
    {

    }

    void OnTriggerEnter(Collider other)
    {
        Debug.Log("PlayerEntered");

        if (other.gameObject.tag == "Player")
        {
            SystemConstants.TriggerCount++;
            Debug.Log("TriggerCount is " + SystemConstants.TriggerCount);

            GameObject Particle = Resources.Load("Prefab/Magic") as GameObject;
            if(Particle == null)
            {
                Debug.Log("Particle is not found");
            }
            Vector3 LocalPosition = this.transform.position;

            Instantiate(Particle, LocalPosition, Quaternion.identity);

            this.GetComponent<BoxCollider>().enabled = false;


            if (SystemConstants.TriggerCount == 5)
            {
                GameObject RedParticle = GameObject.Find("End").transform.GetChild(0).gameObject;
                RedParticle.SetActive(true);
            }

        }


    }



    // Update is called once per frame
    void Update()
    {
        //Debug.Log("CanRun");
    }
}
