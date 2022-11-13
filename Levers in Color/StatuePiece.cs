using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StatuePiece : MonoBehaviour
{
    public float speed = 0.6f;

    public Transform destination;

    public GameObject spawningVFX;

    public GameObject lever;

    private Vector3 originalPosition;
   
    private Vector3 originalScale;

    private Quaternion originalRotation;

    private bool isPickedUp = false;

    private bool isFloating = false;

    private bool isGettingBack = false;

    public Vector3 velocity = Vector3.zero;

    private IEnumerator Floating()
    {
        lever.gameObject.SetActive(true);
        spawningVFX.GetComponent<Lightbeam_Controller>().on = true;
        
        yield return new WaitForSeconds(0.75f);

        spawningVFX.GetComponent<Lightbeam_Controller>().on = false;
        GetBack();
    }

    private IEnumerator StopMoving()
    {
        yield return new WaitForSeconds(10);

        Destroy(this);
    }

    public bool PickedUP()
    {
        if (!isPickedUp)
        {
            isPickedUp = true;
            isFloating = true;
            GetComponent<Collider>().enabled = false;
            StartCoroutine(Floating());

            return true;
        }

        return false;
    }

    public bool GetBack()
    {
        isFloating = false;
        isGettingBack = true;
        StartCoroutine(StopMoving());
        return true;
    }

    // Start is called before the first frame update
    void Start()
    {
        originalPosition = transform.position;
        originalRotation = transform.rotation;
        originalScale = transform.localScale;
    }

    // Update is called once per frame
    void Update()
    {
        if (isFloating)
        {
            transform.position = Vector3.SmoothDamp(transform.position, destination.position, ref velocity, speed);
            transform.rotation = Quaternion.Lerp(transform.rotation, destination.rotation, 2f * Time.deltaTime);
            transform.localScale = Vector3.Lerp(transform.localScale, destination.localScale, 2f * Time.deltaTime);
        }

        if (isGettingBack)
        {
            transform.position = Vector3.SmoothDamp(transform.position, originalPosition, ref velocity, speed);
            transform.rotation = Quaternion.Lerp(transform.rotation, originalRotation, 2f * Time.deltaTime);
            transform.localScale = Vector3.Lerp(transform.localScale, originalScale, 2f * Time.deltaTime);
        }
    }
}
