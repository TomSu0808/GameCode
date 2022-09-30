using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PickUp : MonoBehaviour
{
    private float Collect = 0;

    public TextMeshProUGUI textCollects;

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.transform.tag == "Collect"){
            Collect ++;
            textCollects.text = Collect.ToString();

            Destroy(other.gameObject);
        }
    }
}
