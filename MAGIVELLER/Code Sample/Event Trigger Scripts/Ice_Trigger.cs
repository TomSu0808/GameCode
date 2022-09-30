using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ice_Trigger : MonoBehaviour
{
    public GameObject MoveCube;
    private Animator MoveCubeAnimator;


    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Player")
        {
           MoveCubeAnimator.Play("Push_Cube");
            Debug.Log("It works");
        }
    }
    // Start is called before the first frame update
    void Start()
    {
        MoveCubeAnimator = MoveCube.GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
