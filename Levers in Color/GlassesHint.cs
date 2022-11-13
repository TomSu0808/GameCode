using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GlassesHint : MonoBehaviour
{
    public Player player;

    public GameObject glassesLightbeam;

    public void DisableVFX()
    {
        glassesLightbeam.GetComponent<Lightbeam_Controller>().on = false;
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (Vector3.Distance(player.transform.position, transform.position) < 2f)
            glassesLightbeam.GetComponent<Lightbeam_Controller>().on = false;
        if (Vector3.Distance(player.transform.position, transform.position) > 2f)
            glassesLightbeam.GetComponent<Lightbeam_Controller>().on = true;
    }
}
