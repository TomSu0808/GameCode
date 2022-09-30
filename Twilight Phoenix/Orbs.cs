using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Orbs : CollectTable
{
    [SerializeField] int ordValue = 1;

    protected override void Collected()
    {
        GameManager.MyInstance.AddCollect(ordValue);
        Destroy(this.gameObject);
    }
}
