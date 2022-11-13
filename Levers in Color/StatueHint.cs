using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StatueHint : MonoBehaviour
{
    public Player player;

    public GameObject statueLightbeam;

    public void DisableVFX()
    {
        statueLightbeam.GetComponent<Lightbeam_Controller>().on = false;
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (Vector3.Distance(player.transform.position, transform.position) < 2f)
            statueLightbeam.GetComponent<Lightbeam_Controller>().on = false;
        if (Vector3.Distance(player.transform.position, transform.position) > 2f)
            statueLightbeam.GetComponent<Lightbeam_Controller>().on = true;
    }
}
