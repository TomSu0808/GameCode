using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;

public class ToggleGlasses : MonoBehaviour
{
    public Sprite image1;
    public Sprite image2;
    public Player player;

    public bool glassOn = true;

    private Image image;
    // Start is called before the first frame update
    void Start()
    {
        image = GetComponent<Image>();
    }

    // Update is called once per frame
    void Update()
    {
        if (glassOn)
        {
            player.GetComponent<ColorBlind_Controller>().colorblind = false;
            image.sprite = image1;
        }
        else
        {
            player.GetComponent<ColorBlind_Controller>().colorblind = true;
            image.sprite = image2;
        }
    }

    public void ButtonClick()
    {
        glassOn = !glassOn;
    }
}
