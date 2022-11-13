using JetBrains.Annotations;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lever : MonoBehaviour
{
    public Transform rotationDestination;

    public AudioSource source;

    public AudioClip clip;

    private bool rotating = false;

    private bool rotatingBack = false;

    public bool isFunctioning = false;

    private Quaternion originalRotation;

    public IEnumerator LeverRotation()
    {
        source.PlayOneShot(clip);

        rotating = true;

        yield return new WaitForSeconds(1);

        rotating = false;

        if(!isFunctioning)
            StartCoroutine(LeverRotationBack());
        else
            Destroy(this);
    }

    public IEnumerator LeverRotationBack()
    {
        source.PlayOneShot(clip);

        rotatingBack = true;

        yield return new WaitForSeconds(10);

        rotatingBack = false;
    }

    // Start is called before the first frame update
    void Start()
    {
        originalRotation = transform.rotation;
    }

    // Update is called once per frame
    void Update()
    {
        if(rotating)
        {
            transform.rotation = Quaternion.Lerp(transform.rotation, rotationDestination.rotation, 2f * Time.deltaTime);
        }
        else if(rotatingBack)
        {
            transform.rotation = Quaternion.Lerp(transform.rotation, originalRotation, 2f * Time.deltaTime);
        }
    }
}
