using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lion_Trigger_Entry : MonoBehaviour
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
            SystemConstants.LionCount++;
            Debug.Log("LionCount is " + SystemConstants.LionCount);

            GameObject Particle = this.transform.Find("Lion").transform.GetChild(0).gameObject;
            Particle.SetActive(true);

            this.GetComponent<BoxCollider>().enabled = false;


            if (SystemConstants.LionCount == 4)
            {
                GameObject RedParticle = GameObject.Find("Map4Ent").transform.GetChild(0).gameObject;
                RedParticle.SetActive(true);

                GameObject GreenParticle = GameObject.Find("Map4ElementC").transform.GetChild(0).gameObject;
                GreenParticle.SetActive(true);
            }
            
        }


    }



    // Update is called once per frame
    void Update()
    {
        //Debug.Log("CanRun");
    }
}
