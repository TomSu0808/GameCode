using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pickup : MonoBehaviour
{
    public float speed = 0.6f;

    public Transform destination;

    public bool isPickedUp = false;

    private bool moving = false;

    private Vector3 velocity = Vector3.zero;

    private IEnumerator StopMoving()
    {
        yield return new WaitForSeconds(10);

        if (CompareTag("Glasses"))
            Destroy(this);
        else
            moving = false;
    }

    public bool PickedUP()
    {
        if (!isPickedUp)
        {
            isPickedUp = true;
            moving = true;
            if (CompareTag("Glasses"))
                GetComponent<Collider>().enabled = false;
            StartCoroutine(StopMoving());
            return true;
        }

        return false;
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (moving)
        {
            transform.position = Vector3.SmoothDamp(transform.position, destination.position, ref velocity, speed);
            transform.rotation = Quaternion.Lerp(transform.rotation, destination.rotation, 2f * Time.deltaTime);
            transform.localScale = Vector3.Lerp(transform.localScale, destination.localScale, 2f * Time.deltaTime);
        }
    }
}
