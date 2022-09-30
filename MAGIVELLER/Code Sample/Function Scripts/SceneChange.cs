using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class SceneChange : MonoBehaviour
{
    AsyncOperation asyn;
    Image Load;
    int LoadVal = 0;
    int ProLoadVal = 0;

    public static string NextSceneName;
    void Start()
    {
        Load = GameObject.Find("LoadVal").GetComponent<Image>();

        StartCoroutine(LoadScene());
    }

    void Update()
    {
        if (asyn == null)
        {
            return;
        }
        if (asyn.progress < 0.9f)
        {
            ProLoadVal = (int)asyn.progress * 100;
        }
        else
        {
            ProLoadVal = 100;
        }
        if (LoadVal < ProLoadVal)
        {
            LoadVal++;
            Load.fillAmount = LoadVal / 100f;
            if (LoadVal == 100)
            {
                asyn.allowSceneActivation = true;
            }
        }
    }
    IEnumerator LoadScene()
    {
        yield return new WaitForSeconds(0.1f);
        asyn = SceneManager.LoadSceneAsync(NextSceneName);
        asyn.allowSceneActivation = false;
    }
}
