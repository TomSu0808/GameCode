using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class UIManager : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI txtCollects, txtVictoryCondition;
    [SerializeField] GameObject victoryCondition;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            DestroyImmediate(this);
        }
    }

    private static UIManager instance;

    public static UIManager MyInstance
    {
        get
        {
            if (instance == null)
                instance = new UIManager();

            return instance;
        }
    }

    public void UpdateCollectUI(int _collects, int _victoryCondition)
    {
        txtCollects.text = "Orbs: " + _collects + " / " + _victoryCondition;
    }

    public void ShowVictoryCondition(int _collects, int _victoryCondition)
    {
        victoryCondition.SetActive(true);
        txtVictoryCondition.text = "You need " + (_victoryCondition - _collects) + " more Ords";
    }

    public void HideVictoryCondition()
    {
        victoryCondition.SetActive(false);
    }
}
