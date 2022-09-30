using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    private int collectedCollects, victoryCondition = 3;

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

    private static GameManager instance;

    public static GameManager MyInstance
    {
        get
        {
            if(instance == null)
                instance = new GameManager();

            return instance;
        }
    }

   private void Start()
    {
        UIManager.MyInstance.UpdateCollectUI(collectedCollects, victoryCondition);
    }

    public void AddCollect(int _collects)
    {
        collectedCollects += _collects;
       // Debug.Log(collects);
        UIManager.MyInstance.UpdateCollectUI(collectedCollects, victoryCondition);
    }

}
