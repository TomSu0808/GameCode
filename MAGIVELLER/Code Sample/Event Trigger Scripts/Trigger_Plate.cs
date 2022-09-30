using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Trigger_Plate : MonoBehaviour
{
    public bool isUp = false;
    private GameObject WaterBody;
    public GameObject Spree;
    public GameObject Spree2;
    private Animator Anim;
    
    // Start is called before the first frame update
    void Start()
    {
        Anim = this.GetComponent<Animator>();
        WaterBody = GameObject.Find("JiguanWater1");
        Spree = GameObject.Find("Eff1").transform.GetChild(0).gameObject;
        Spree2 = GameObject.Find("Eff2").transform.GetChild(0).gameObject;
    }


    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Player")
        {
            Anim.Play("Rock_Pressure");
            Debug.Log("It works");
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.tag == "Player")
        {
            Anim.Play("Rock_Relese");
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.tag == "Player")
        {
            Vector3 WaterPosition = WaterBody.transform.position;

            switch (isUp)
            {
                case true:

                    if(WaterBody.transform.position.y != SystemConstants.MaxWaterLevel)
                    {
                        if (WaterBody.transform.position.y < SystemConstants.MaxWaterLevel)
                        {
                            WaterPosition.y += Time.deltaTime;
                            WaterBody.transform.position = WaterPosition;
                        }

                        if (WaterBody.transform.position.y > SystemConstants.MaxWaterLevel)
                        {
                            WaterPosition.y = SystemConstants.MaxWaterLevel;
                            WaterBody.transform.position = WaterPosition;
                        }
                    }

                    if (WaterBody.transform.position.y == SystemConstants.MaxWaterLevel)
                    {
                        Spree.SetActive(true);
                        Spree2.SetActive(true);

                    }

                    break;
                case false:

                    if (WaterBody.transform.position.y != SystemConstants.MinWaterLevel)
                    {
                        if (WaterBody.transform.position.y > SystemConstants.MinWaterLevel)
                        {
                            WaterPosition.y -= Time.deltaTime;
                            WaterBody.transform.position = WaterPosition;
                        }

                        if (WaterBody.transform.position.y < SystemConstants.MinWaterLevel)
                        {
                            WaterPosition.y = SystemConstants.MinWaterLevel;
                            WaterBody.transform.position = WaterPosition;
                        }
                    }

                    break;

            }
        }

    }



    // Update is called once per frame
    void Update()
    {
        
    }
}
