using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IceMap_Trigger_Entry : MonoBehaviour
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

            GameObject Particle = Resources.Load("Prefab/Eff_Fire") as GameObject;
            if(Particle == null)
            {
                Debug.Log("Particle is not found");
            }
            Vector3 LocalPosition = this.transform.position;

            Instantiate(Particle, LocalPosition, Quaternion.identity);

            this.GetComponent<BoxCollider>().enabled = false;


            if (SystemConstants.TriggerCount == 4)
            {
                GameObject IceParticle = GameObject.Find("Eff_Ice").transform.GetChild(0).gameObject;
                IceParticle.SetActive(true);

                GameObject ZS = GameObject.Find("ZS1").transform.GetChild(0).gameObject;
                ZS.SetActive(true);

            }

        }


    }



    // Update is called once per frame
    void Update()
    {
        //Debug.Log("CanRun");
    }
}
