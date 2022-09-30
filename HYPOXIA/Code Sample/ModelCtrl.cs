using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

public class ModelCtrl : MonoBehaviour {

	public bool 可交互 = false;

	public float timer = 0f;
	public float scale = 1.5f;
	
	// Update is called once per frame
	void Update () {

		if (可交互)
		{
			if (Input.GetKeyDown(KeyCode.F))
			{
				this.transform.DOScale(scale, timer).SetLoops(-1, LoopType.Yoyo);
			}
		}
	}
}
