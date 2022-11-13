using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;
using static UnityEngine.Rendering.DebugUI;

public class Player : MonoBehaviour
{
    public float speed = 0.8f;
    public GameObject fade;
    private int collectedPieces = 0;
    private int leversPulled = 0;

    public GameObject toggleGlasses;

    public GameObject exitButton;

    public GameObject startPointHint1;

    public GameObject statueHint;

    public GameObject glassesBreakingVFX;

    public AudioSource source;

    public AudioClip tapping;

    private Vector3 velocity = Vector3.zero;

    private bool move = false;

    private Transform destination;

    GameObject[] POIs;

    IEnumerator ShowExitButton()
    {
        yield return new WaitForSeconds(10);

        exitButton.SetActive(true);
    }

    IEnumerator PickUpGlasses()
    {
        glassesBreakingVFX.GetComponent<Lightbeam_Controller>().on = true;

        yield return new WaitForSeconds(0.75f);

        glassesBreakingVFX.GetComponent<Lightbeam_Controller>().on = false;
    }

    // Start is called before the first frame update
    void Start()
    {
        POIs = GameObject.FindGameObjectsWithTag("StandPoint");
        foreach (GameObject POI in POIs)
        {
            if (Vector3.Distance(POI.transform.position, transform.position) < 2f || Vector3.Distance(POI.transform.position, transform.position) > POI.GetComponentInChildren<Button>().showDistance)
                POI.SetActive(false);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit, 100.0f))
            {
                if (hit.transform.gameObject.CompareTag("StandPoint"))
                {
                    destination = hit.transform;
                    move = true;
                    foreach (GameObject POI in POIs)
                    {
                        POI.SetActive(false);
                    }
                }

                else if (hit.transform.gameObject.CompareTag("Glasses"))
                {
                    source.PlayOneShot(tapping);
                    if (hit.transform.gameObject.GetComponent<Pickup>().PickedUP() == true)
                    {
                        collectedPieces++;
                    }

                    if (collectedPieces == 3)
                    {
                        startPointHint1.GetComponent<GlassesHint>().enabled = true;
                    }

                    if (hit.transform.gameObject.name == "Pickup Lense (1)")
                    {
                        startPointHint1.GetComponent<LensHint>().DisableVFX();
                        Destroy(startPointHint1.GetComponent<LensHint>());
                    }
                }

                else if (hit.transform.gameObject.name == "Pickup Frame_Destination")
                {
                    if (collectedPieces == 3)
                    {
                        // Collect the Glasses
                        source.PlayOneShot(tapping);
                        StartCoroutine(PickUpGlasses());
                        startPointHint1.GetComponent<GlassesHint>().DisableVFX();
                        Destroy(startPointHint1.GetComponent<GlassesHint>());
                        Destroy(hit.transform.gameObject);
                        toggleGlasses.gameObject.SetActive(true);
                        statueHint.GetComponent<StatueHint>().enabled = true;
                    }
                }

                else if (hit.transform.gameObject.name == "Statue Piece")
                {
                    source.PlayOneShot(tapping);
                    if (hit.transform.gameObject.GetComponent<StatuePiece>().PickedUP() == true)
                    {
                        statueHint.GetComponent<StatueHint>().DisableVFX();
                        Destroy(statueHint.GetComponent<StatueHint>());
                    }
                }

                else if (hit.transform.gameObject.name == "Lever Base")
                {
                    //fade.GetComponent<Fade>().FadeShow();

                }

                else if (hit.transform.gameObject.CompareTag("Lever"))
                {
                    if (hit.transform.gameObject.GetComponent<Pickup>().PickedUP() == false)
                    {
                        StartCoroutine(hit.transform.gameObject.GetComponent<Lever>().LeverRotation());
                        if (hit.transform.gameObject.GetComponent<Lever>().isFunctioning)
                            leversPulled++;
                        if (leversPulled == 2)
                        {
                            // End Scene;
                            gameObject.GetComponent<Cutscene>().playScene = true;
                            toggleGlasses.SetActive(false);
                            foreach (GameObject POI in POIs)
                            {
                                POI.SetActive(false);
                            }
                            StartCoroutine(ShowExitButton());
                        }
                    }
                    else
                    {
                        source.PlayOneShot(tapping);

                        GameObject[] levers = GameObject.FindGameObjectsWithTag("Lever");

                        foreach (GameObject lever in levers)
                        {
                            lever.GetComponent<Lever>().isFunctioning = true;
                        }
                    }
                }
            }
        }

        if (move == true)
        {
            transform.position = Vector3.SmoothDamp(transform.position, destination.position, ref velocity, speed);
            //transform.position = Vector3.Lerp(transform.position, destination.position, 2 * Time.deltaTime);
            //transform.position = Vector3.MoveTowards(transform.position, destination.position, 10f * Time.deltaTime);

            if ((int)transform.position.x == (int)destination.position.x && (int)transform.position.z == (int)destination.position.z)
            {
                move = false;
                foreach (GameObject POI in POIs)
                {
                    if (Vector3.Distance(POI.transform.position, transform.position) > 2f && Vector3.Distance(POI.transform.position, transform.position) < POI.GetComponentInChildren<Button>().showDistance)
                    {
                        if (POI.GetComponent<Button>() != null)
                            POI.GetComponent<Button>().SetPos();
                        POI.SetActive(true);
                    }
                }
            }
        }
    }
}
